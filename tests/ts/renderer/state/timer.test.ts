import { reducer } from "sanascan/renderer/state";
import { initialState } from "./initialState";

describe("isActiveが設定できる", () => {
  for (const i of [true, false]) {
    test( i.toString() + "の場合", () => {
      const isActive = i;
      const result = reducer(
        initialState,
        {
          payload: { isActive },
          type: "sanascan/timer/SET_ACTIVE",
        },
      );
      expect(result).toMatchSnapshot();
    });
  }
});

test("idが設定できる", () => {
  const id = 1234;
  const result = reducer(
    initialState,
    {
      payload: { id },
      type: "sanascan/timer/SET_ID",
    },
  );
  expect(result).toMatchSnapshot();
});

test("scanSpeedが設定できる", () => {
  const scanSpeed = 500;
  const result = reducer(
    initialState,
    {
      payload: { scanSpeed },
      type: "sanascan/timer/SET_SCAN_SPEED",
    },
  );
  expect(result).toMatchSnapshot();
});
