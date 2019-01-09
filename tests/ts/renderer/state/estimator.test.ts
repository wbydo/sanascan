import snapshotDiff from "snapshot-diff";

import { reducer } from "sanascan/renderer/state";
import { actions } from "sanascan/renderer/state/estimator";

import { initialState } from "./initialState";

test("idが設定できる", () => {
  const id = 1234;
  const result = reducer(
    initialState,
    actions.setId(id),
  );
  expect(
    snapshotDiff( initialState, result),
  ).toMatchSnapshot();
});

test("resultを設定できる", () => {
  const content = "あらゆる現実を全て自分の方へねじ曲げたのだ";
  const result = reducer(
    initialState,
    actions.setResult(content),
  );
  expect(
    snapshotDiff( initialState, result),
  ).toMatchSnapshot();
});
