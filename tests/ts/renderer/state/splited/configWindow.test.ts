import { store } from "sanascan/renderer/state";
import { reducer } from "sanascan/renderer/state";

test("isActiveが設定できる", () => {
  for (const i of [true, false]) {
    const isActive = i;
    const result = reducer(
      undefined,
      {
        payload: { isActive },
        type: "sanascan/configWindow/SET_ACTIVE",
      },
    );
    expect(result.configWindow.isActive).toEqual(isActive);
  }
});
