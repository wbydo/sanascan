import * as types from "./types";

export interface Action {
  type: string;
}

export const increment: () => Action = () => {
  return {
    type: types.INCREMENT,
  };
};
