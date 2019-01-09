import { reducer } from "sanascan/renderer/state";

import { initialState } from "./initialState";

describe("isActiveが設定できる", () => {
  for (const i of [true, false]) {
    test(i.toString() + "の場合", () => {
      const isActive = i;
      const result = reducer(
        initialState,
        {
          payload: { isActive },
          type: "sanascan/configWindow/SET_ACTIVE",
        },
      );
      expect(result).toMatchSnapshot();
    });
  }

});
