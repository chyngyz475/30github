import produce from "immer";

type State = {
    count: number;
    todos: { id: number; text: string; completed: boolean }[];
};

const initialState: State = {
    count: 0,
    todos: []
};

const reducer = (state = initialState, action: any) =>
    produce(state, (draft) => {
        switch (action.type) {
            case "INCREMENT":
                draft.count += 1;
                break;
            case "ADD_TODO":
                draft.todos.push({ id: Date.now(), text: action.text, completed: false });
                break;
            case "TOGGLE_TODO":
                const todo = draft.todos.find((t) => t.id === action.id);
                if (todo) {
                    todo.completed = !todo.completed;
                }
                break;
        }
    });
