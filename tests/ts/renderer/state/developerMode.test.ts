import snapshotDiff from "snapshot-diff";

import { reducer } from "sanascan/renderer/redux";
import { actions } from "sanascan/renderer/redux/state/developerMode";

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

describe("estimatorIsActiveが設定できる", () => {
  for (const i of [true, false]) {
    test( i.toString() + "の場合", () => {
      const result = reducer(
        initialState,
        actions.setEstimatorActivity(i),
      );
      expect(
        snapshotDiff( initialState, result),
      ).toMatchSnapshot();
    });
  }
});
