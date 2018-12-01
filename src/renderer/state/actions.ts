import * as types from "./types";

export interface Action {
  error: boolean;
  type: string;
}

export const activateConfigure: () => Action = () => {
  return {
    error: false,
    type: types.ACTIVATE_CONFIGURE_WINDOW,
  };
};

export const deactivateConfigure: () => Action = () => {
  return {
    error: false,
    type: types.DEACTIVATE_CONFIGURE_WINDOW,
  };
};
