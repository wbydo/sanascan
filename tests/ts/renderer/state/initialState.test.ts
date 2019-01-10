import { initialState } from "./initialState";

test("initialState", () => {
  expect(initialState).toMatchSnapshot();
});
