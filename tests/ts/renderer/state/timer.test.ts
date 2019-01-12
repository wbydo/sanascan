import snapshotDiff from "snapshot-diff";

import { reducer } from "sanascan/renderer/redux";
import { actions } from "sanascan/renderer/redux/state/timer";

import { initialState } from "./initialState";

test("scanSpeedが設定できる", () => {
  const scanSpeed = 234;
  const result = reducer(
    initialState,
    actions.setScanSpeed(scanSpeed),
  );
  expect(
    snapshotDiff( initialState, result),
  ).toMatchSnapshot();
});
