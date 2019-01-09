import snapshotDiff from "snapshot-diff";

import { store } from "sanascan/renderer/state";
import { reducer } from "sanascan/renderer/state";

import { MAX_COLUMN_INDEX } from "sanascan/renderer/constant";

import { initialState } from "./initialState";

test("activeColumnが1増える", () => {
  const result = reducer(
    initialState,
    {type: "sanascan/cursol/INCREMENT" },
  );

  expect(
    snapshotDiff( initialState, result),
  ).toMatchSnapshot();
});

test("activeColumnが0に戻る", () => {
  const x = MAX_COLUMN_INDEX;
  const state = { ...store.getState(), cursol: {activeColumn: x}};
  const result = reducer(
    state,
    {type: "sanascan/cursol/INCREMENT" },
  );

  expect(
    snapshotDiff(state, result),
  ).toMatchSnapshot();
});
