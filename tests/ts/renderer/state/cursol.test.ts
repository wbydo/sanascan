import { store } from "sanascan/renderer/state";
import { reducer } from "sanascan/renderer/state";

import { MAX_COLUMN_INDEX } from "sanascan/renderer/constant";

test("activeColumnが1増える", () => {
  const x = 5;
  const initialState = { ...store.getState(), cursol: {activeColumn: x}};
  const result = reducer(
    initialState,
    {type: "sanascan/cursol/INCREMENT" },
  );

  const target = { ...store.getState(), cursol: {activeColumn: x + 1}};
  expect(result).toEqual(target);
});

test("activeColumnが0に戻る", () => {
  const x = MAX_COLUMN_INDEX;
  const initialState = { ...store.getState(), cursol: {activeColumn: x}};
  const result = reducer(
    initialState,
    {type: "sanascan/cursol/INCREMENT" },
  );

  const target = { ...store.getState(), cursol: {activeColumn: 0}};
  expect(result).toEqual(target);
});
