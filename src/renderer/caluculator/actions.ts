import * as types from "./types";

export interface CaluculatorAction {
  type: string;
  value: number;
}

export const input: (value: number) => CaluculatorAction = (value) => {
  return({
    type: types.INPUT_FIGURE,
    value,
  });
};

export class ActionDispatcher {
  constructor(private dispatch: (action: CaluculatorAction) => void) {}

  public input(value: number) {
    this.dispatch(input(value));
  }
}
