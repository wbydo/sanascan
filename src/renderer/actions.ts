import * as types from "./types";

export interface Action {
  type: string;
}

export const increment: () => Action = () => {
  return {
    type: types.INCREMENT,
  };
};

export const incrementAsync: () => Action = () => {
  return {
    type: types.ASYNC_INCREMENT,
  };
};
