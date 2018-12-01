import * as types from "./types";

export interface Action {
  error: boolean;
  type: string;
}

export const increment: () => Action = () => {
  return {
    error: false,
    type: types.INCREMENT,
  };
};
