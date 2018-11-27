import * as types from "./types";

export interface Action {
  type: string;
}

export const increment: () => Action = () => {
  return {
    type: types.INCREMENT,
  };
};

export const startIncrement: () => Action = () => {
  return {
    type: types.START_INCREMENT,
  };
};
