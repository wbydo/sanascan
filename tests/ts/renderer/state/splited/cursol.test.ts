import { store } from "sanascan/renderer/state";
import { reducer } from "sanascan/renderer/state";

test("activeColumnが1増える", () => {
  const x = 5;
  const initialState = { ...store.getState(), cursol: {activeColumn: x}};
  const result = reducer(
    initialState,
    {type: "sanascan/cursol/INCREMENT" },
  );
  expect(result.cursol.activeColumn).toEqual(1);
});
