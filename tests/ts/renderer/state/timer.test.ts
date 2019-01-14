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

describe("isActiveが設定できる", () => {
  for (const i of [true, false]) {
    test( i.toString() + "の場合", () => {
      const result = reducer(
        initialState,
        actions.setActive(i),
      );
      expect(
        snapshotDiff( initialState, result),
      ).toMatchSnapshot();
    });
  }
});
