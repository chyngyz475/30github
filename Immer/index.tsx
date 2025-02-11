import produce from "immer";

const state = {
  todos: [{ id: 1, text: "Купить хлеб", completed: false }]
};

const newState = produce(state, (draft) => {
  draft.todos.push({ id: 2, text: "Выучить Immer", completed: false });
});

console.log(newState.todos); 
// [
//   { id: 1, text: "Купить хлеб", completed: false },
//   { id: 2, text: "Выучить Immer", completed: false }
// ]
