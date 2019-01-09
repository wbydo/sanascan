import { reducer } from "sanascan/renderer/state";
import { initialState } from "./initialState";

test("idが設定できる", () => {
  const id = 1234;
  const result = reducer(
    initialState,
    {
      payload: { id },
      type: "sanascan/estimator/SET_ID",
    },
  );
  expect(result).toMatchSnapshot();
});

test("resultを設定できる", () => {
  const content = "あらゆる現実を全て自分の方へねじ曲げたのだ";
  const result = reducer(
    initialState,
    {
      payload: { content },
      type: "sanascan/estimator/SET_RESULT",
    },
  );
  expect(result).toMatchSnapshot();
});
