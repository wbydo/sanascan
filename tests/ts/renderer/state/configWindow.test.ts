import { reducer } from "sanascan/renderer/state";
import { actions } from "sanascan/renderer/state/configWindow";

import { initialState } from "./initialState";

describe("isActiveが設定できる", () => {
  for (const i of [true, false]) {
    test(i.toString() + "の場合", () => {
      const result = reducer(
        initialState,
        actions.setActive(i),
      );
      expect(result).toMatchSnapshot();
    });
  }

});
