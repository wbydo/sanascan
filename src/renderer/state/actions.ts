import * as types from "./types";

export interface Action {
  type: string;
}

export const activateConfigure: () => Action = () => {
  return {
    type: types.ACTIVATE_CONFIGURE,
  };
};

export const deactivateConfigure: () => Action = () => {
  return {
    type: types.DEACTIVATE_CONFIGURE,
  };
};
