from operator import attrgetter
from typing import Iterable, List

from antibot.provided import DISMISS_BUTTON
from antibot.slack.message import Block, Element, Option, OptionGroup, ActionStyle, Confirm
from boxdenat.actions import BoxActions
from boxdenat.menu.model import Menu
from boxdenat.orders import Order
from boxdenat.points import compute_points, UserPoints


class BoxUi:
    def menu(self, date: str, menu: Menu) -> Iterable[Block]:
        text = f'*Menu du {date}*\n'
        for box in menu.boxes:
            text += f'• {box} - {box.price}€\n'
        if menu.soup is not None:
            text += f'• {menu.soup} - {menu.soup.price}€'
        text += '\n*Desserts :*\n'
        for dessert in menu.desserts:
            if len(dessert.flavors) > 0:
                flavors = ', '.join(dessert.flavors)
                text += f'• {dessert.name} ({flavors})\n'
            else:
                text += f'• {dessert.name}\n'

        yield Block.section(text)
        yield Block.actions(
            Element.button(BoxActions.create_order, 'Place an order')
        )

    def order_summary(self, order: Order) -> str:
        items = order.all_items()
        total_price = sum(map(attrgetter('price'), items))
        points = compute_points(order)
        if len(items) == 0:
            return 'Your order is empty'

        items = [f'• {item}\n' for item in items]

        return ''.join(items) + f'\nTotal price : {total_price}€ ({points} points)'

    def my_order(self, menu: Menu, order: Order) -> Iterable[Block]:
        yield Block.section(self.order_summary(order))

        validate_button = Element.button(BoxActions.order_confirm, 'Validate', ActionStyle.primary)
        cancel_button = Element.button(BoxActions.order_cancel, 'Cancel', ActionStyle.danger)
        edit_button = Element.button(BoxActions.order_edit, 'Modify')
        cancel_button_confirm = Element.button(BoxActions.order_cancel, 'Cancel', ActionStyle.danger,
                                               confirm=Confirm.of('Delete order', 'Delete this order', 'Yes', 'No'))
        main_actions = []
        if not order.in_edition:
            main_actions.append(edit_button)
        else:
            main_actions.append(validate_button)
        if order.complete:
            main_actions.append(cancel_button_confirm)
        else:
            main_actions.append(cancel_button)
        main_actions.append(DISMISS_BUTTON)

        yield Block.actions(*main_actions)

        if not order.in_edition:
            return

        options = [Option.of(str(hash(box)), box.name) for box in menu.boxes]
        yield Block.actions(
            Element.select(BoxActions.add_box, 'Pick a box...', options),
            Element.button(BoxActions.clear_box, 'Clear boxes')
        )

        options = []
        generic_group = []
        for dessert in menu.desserts:
            if len(dessert.flavors) > 0:
                values = [Option.of(str(hash(df)), str(df)) for df in dessert.iter_flavors()]
                group = OptionGroup.of(dessert.name, values)
                options.append(group)
            else:
                df = dessert.with_flavor(None)
                generic_group.append(Option.of(str(hash(df)), str(df)))

        options.insert(0, OptionGroup.of('Simple Desserts', generic_group))
        yield Block.actions(
            Element.group_select(BoxActions.add_dessert, 'Pick a dessert...', options),
            Element.button(BoxActions.clear_dessert, 'Clear desserts')
        )

    def all_orders(self, orders: List[Order]) -> Iterable[Block]:
        for order in orders:
            text = f'*{order.user.display_name}*\n'
            text += '\n'.join([f'• {item}' for item in order.all_items()])
            yield Block.section(text)
            yield Block.divider()

    def points(self, pref_user: UserPoints, user_points: Iterable[UserPoints]) -> Iterable[Block]:
        text = [f'• {up.user.display_name} : {up.points} points' for up in user_points]
        if text:
            yield Block.section('\n'.join(text))
        else:
            yield Block.section('No points')

        if pref_user:
            yield Block.actions(
                Element.button(BoxActions.free_box, 'Give a free box', ActionStyle.primary,
                               confirm=Confirm.of('Free Box',
                                                  f'Give a free box to {pref_user.user.display_name}',
                                                  'Yes', 'No')),
                DISMISS_BUTTON
            )

        else:
            yield Block.actions(DISMISS_BUTTON)
