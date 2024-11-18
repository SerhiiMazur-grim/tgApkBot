from aiogram.fsm.context import FSMContext


async def clear_state(state: FSMContext) -> None:
    current_state = await state.get_state()
        
    if current_state is not None:
        await state.clear()
