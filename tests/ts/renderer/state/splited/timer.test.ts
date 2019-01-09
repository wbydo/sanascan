import { reducer } from "sanascan/renderer/state";

test("isActiveが設定できる", () => {
  for (const i of [true, false]) {
    const isActive = i;
    const result = reducer(
      undefined,
      {
        payload: { isActive },
        type: "sanascan/timer/SET_ACTIVE",
      },
    );
    expect(result.timer.isActive).toEqual(isActive);
  }
});

test("idが設定できる", () => {
  const id = 1234;
  const result = reducer(
    undefined,
    {
      payload: { id },
      type: "sanascan/timer/SET_ID",
    },
  );
  expect(result.timer.id).toEqual(id);
});

test("scanSpeedが設定できる", () => {
  const scanSpeed = 500;
  const result = reducer(
    undefined,
    {
      payload: { scanSpeed },
      type: "sanascan/timer/SET_SCAN_SPEED",
    },
  );
  expect(result.timer.scanSpeed).toEqual(scanSpeed);
});
