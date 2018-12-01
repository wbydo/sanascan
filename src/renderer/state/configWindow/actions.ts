import * as types from "./types";

export interface Action {
  error: boolean;
  type: string;
  payload?: {
    isActive: boolean;
  };
}

export const setActive = (isActive: boolean): Action => {
  return {
    error: false,
    payload: {
      isActive,
    },
    type: types.SET_ACTIVE,
  };
};
