from dataclasses import replace
from typing import Optional

from injector import inject

from antibot.decorators import command, block_action, daily
from antibot.internal.slack.channel import Channel
from antibot.plugin import AntibotPlugin
from antibot.repository.messages import MessagesRepository, SlackMessage
from antibot.slack.api import SlackApi
from antibot.slack.callback import BlockAction
from antibot.slack.message import Message, Block
from antibot.tools import today, yesterday
from antibot.user import User
from boxdenat.actions import BoxActions
from boxdenat.menu.model import Box, DessertWithFlavor
from boxdenat.menu.provider import MenuProvider
from boxdenat.orders import OrderRepository, Order
from boxdenat.points import PointsRepository, compute_points
from boxdenat.ui import BoxUi


class BoxPlugin(AntibotPlugin):
    @inject
    def __init__(self, menu_provider: MenuProvider, orders: OrderRepository, api: SlackApi, ui: BoxUi,
                 messages: MessagesRepository, points: PointsRepository):
        super().__init__('Box')
        self.menu_provider = menu_provider
        self.orders = orders
        self.api = api
        self.ui = ui
        self.messages = messages
        self.points = points

    @property
    def menu(self):
        return self.menu_provider.get()

    @command('/box')
    def main(self, user: User, channel: Channel, params: str):
        params = params.split(' ')

        cmd = params[0]
        args = params[1:]
        if cmd == 'menu':
            return self.display_menu()
        elif cmd == 'order':
            return self.create_new_order(user)
        elif cmd == 'call':
            return self.display_orders(channel)
        elif cmd == 'points':
            return self.display_points()
        elif cmd == 'free':
            return self.free_box()
        elif cmd == 'charge':
            return self.charge_box()
        else:
            return self.display_help()

    def display_help(self):
        return Message.ephemeral([
            Block.section('''*Available commands :*
            • help : display this message
            • menu : display today's menu
            • order : place an order
            • call : display current orders
            • points : display points
            • free : there is a free box available
            • charge : an additional TR is required
            ''')
        ])

    @command('/box/menu')
    def display_menu(self):
        self.menu_provider.get()
        blocks = self.ui.menu(self.menu_provider.date, self.menu)
        return Message(f'Menu for {self.menu_provider.date}', blocks=list(blocks))

    @block_action(action_id=BoxActions.create_order)
    def create_new_order(self, user: User):
        order = self.orders.find(today(), user)
        if order is None:
            order = self.orders.create(user)
        return Message.ephemeral(self.ui.my_order(self.menu, order))

    @block_action(action_id=BoxActions.add_box)
    def add_box(self, action: BlockAction, user: User):
        order = self.orders.find(today(), user)
        box = self.find_box(action.selected_option.value)
        if box:
            order = replace(order, boxes=order.boxes + [box])
        self.orders.update(order)

        return Message.replace(self.ui.my_order(self.menu, order))

    def find_box(self, id) -> Optional[Box]:
        for box in self.menu.boxes:
            if str(hash(box)) == id:
                return box

        return None

    @block_action(action_id=BoxActions.clear_box)
    def clear_box(self, user: User):
        order = self.orders.find(today(), user)
        order = replace(order, boxes=[])
        self.orders.update(order)

        return Message.replace(self.ui.my_order(self.menu, order))

    @block_action(action_id=BoxActions.add_dessert)
    def add_dessert(self, action: BlockAction, user: User):
        order = self.orders.find(today(), user)
        dessert = self.find_dessert(action.selected_option.value)
        if dessert:
            order = replace(order, desserts=order.desserts + [dessert])
        self.orders.update(order)

        return Message.replace(self.ui.my_order(self.menu, order))

    def find_dessert(self, id) -> Optional[DessertWithFlavor]:
        for dessert in self.menu.all_desserts():
            if str(hash(dessert)) == id:
                return dessert

        return None

    @block_action(action_id=BoxActions.clear_dessert)
    def clear_dessert(self, user: User):
        order = self.orders.find(today(), user)
        order = replace(order, desserts=[])
        self.orders.update(order)

        return Message.replace(self.ui.my_order(self.menu, order))

    @block_action(action_id=BoxActions.order_confirm)
    def order_confirm(self, channel: Channel, user: User):
        order = self.orders.find(today(), user)
        new_order = not order.complete
        points = self.update_points(order)
        order = replace(order, complete=True, in_edition=False, points_given=points)
        self.orders.update(order)
        self.complete_order(channel, user, new_order)

        return Message.replace(self.ui.my_order(self.menu, order))

    def update_points(self, order: Order) -> int:
        order_points = compute_points(order)
        add_points = order_points - order.points_given
        self.points.update(order.user, add_points)
        return order_points

    def complete_order(self, channel: Channel, user: User, new_order: bool):
        cmds = list(self.messages.find_all('orders', date=today()))
        if len(cmds) == 0:
            cmds = [self.display_orders(channel)]
        link = self.api.get_permalink(cmds[-1].channel_id, cmds[-1].timestamp)
        if new_order:
            message = f'{user.display_name} placed an order\n<{link}|View all orders>'
        else:
            message = f'{user.display_name} updated an order\n<{link}|View all orders>'
        self.api.post_message(channel.id, Message(message))
        self.update_displayed_orders(channel)

    def display_orders(self, channel: Channel) -> SlackMessage:
        orders = list(self.orders.find_all(today()))
        reply = self.api.post_message(channel.id, Message(blocks=list(self.ui.all_orders(orders))))
        message = SlackMessage.create_today('orders', reply.ts, reply.channel)
        self.messages.create(message)
        return message

    def update_displayed_orders(self, channel: Channel):
        orders = list(self.orders.find_all(today()))
        for cmd_message in self.messages.find_all('orders', date=today()):
            new_ts = self.api.update_message(channel.id, cmd_message.timestamp,
                                             Message(blocks=list(self.ui.all_orders(orders)))).ts
            self.messages.update_timestamp(cmd_message.id, new_ts)

    @block_action(action_id=BoxActions.order_cancel)
    def order_cancel(self, user: User):
        order = self.orders.find(today(), user)
        self.orders.delete(order.id)
        self.points.update(order.user, -1 * order.points_given)
        return Message.delete()

    @block_action(action_id=BoxActions.order_edit)
    def order_edit(self, user: User):
        order = self.orders.find(today(), user)
        order = replace(order, in_edition=True)
        self.orders.update(order)
        return Message.replace(self.ui.my_order(self.menu, order))

    @daily(hour='02:00')
    def reset(self):
        for order in self.orders.find_all(yesterday()):
            self.orders.delete(order.id)
        for message in self.messages.find_all(type='orders', date=yesterday()):
            self.messages.delete(message.id)

    def display_points(self):
        return Message(blocks=list(self.ui.points(self.points.pref_user(), self.points.find_all())))

    @block_action(action_id=BoxActions.free_box)
    def free_box(self):
        pref_user = self.points.pref_user()
        self.points.update(pref_user.user, -85)
        return Message(f'<@{pref_user.user.id}> receives a free box and had 85 points deducted',
                       replace_original=True)

    def charge_box(self):
        pref_user = self.points.least_user()
        self.points.update(pref_user.user, 85)
        return Message(f'<@{pref_user.user.id}> needs to pay an additional TR and was credited 85 points',
                       replace_original=True)
