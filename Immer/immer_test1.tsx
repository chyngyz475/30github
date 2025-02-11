import produce from "immer";
import { initialState, reducer } from "./reducer";

test("INCREMENT увеличивает count", () => {
    const action = { type: "INCREMENT" };
    const newState = reducer(initialState, action);
    expect(newState.count).toBe(1);
});

test("ADD_TODO добавляет новый todo", () => {
    const action = { type: "ADD_TODO", text: "Новая задача" };
    const newState = reducer(initialState, action);
    expect(newState.todos.length).toBe(1);
    expect(newState.todos[0].text).toBe("Новая задача");
});

test("TOGGLE_TODO переключает статус", () => {
    const state = produce(initialState, (draft) => {
        draft.todos.push({ id: 1, text: "Тест", completed: false });
    });

    const action = { type: "TOGGLE_TODO", id: 1 };
    const newState = reducer(state, action);
    expect(newState.todos[0].completed).toBe(true);
});
