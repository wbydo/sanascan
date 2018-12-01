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

export const runMiddleware = (): Action => {
  return {
    error: false,
    type: types.RUN_MIDDLEWARE,
  };
};
