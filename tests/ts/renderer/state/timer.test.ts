import snapshotDiff from "snapshot-diff";

import { reducer } from "sanascan/renderer/state";
import { actions } from "sanascan/renderer/state/timer";

import { initialState } from "./initialState";

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
