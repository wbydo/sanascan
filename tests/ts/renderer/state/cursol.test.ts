import snapshotDiff from "snapshot-diff";

import { store } from "sanascan/renderer/state";
import { reducer } from "sanascan/renderer/state";

import { actions } from "sanascan/renderer/state/cursol";

import { MAX_COLUMN_INDEX } from "sanascan/renderer/constant";

import { initialState } from "./initialState";

test("activeColumnが1増える", () => {
  const result = reducer(
    initialState,
    actions.increment(),
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
    actions.increment(),
  );

  expect(
    snapshotDiff(state, result),
  ).toMatchSnapshot();
});
