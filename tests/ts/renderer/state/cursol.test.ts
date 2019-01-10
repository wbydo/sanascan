import snapshotDiff from "snapshot-diff";

import { reducer } from "sanascan/renderer/redux";

import { actions } from "sanascan/renderer/redux/state/cursol";

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
  const state = {
    ...initialState,
    cursol: {
      ...initialState.cursol,
      activeColumn: x,
    },
  };

  const result = reducer(
    state,
    actions.increment(),
  );

  expect(
    snapshotDiff(state, result),
  ).toMatchSnapshot();
});

describe("modeが設定出来る", () => {
  const thisTest = (i: "normal" | "proposed") => {
    test(i + "の場合", () => {
      const result = reducer(
        initialState,
        actions.setMode(i),
      );

      expect(
        snapshotDiff( initialState, result),
      ).toMatchSnapshot();
    });
  };

  const normal = "normal";
  thisTest(normal);

  const proposed = "proposed";
  thisTest(proposed);
});
