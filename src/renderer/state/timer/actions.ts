import * as types from "./types";

export interface Action {
  type: string;
  payload?: {
    isActive?: boolean,
    scanSpeed?: number,
  };
  error: boolean;
}

export const start: () => Action = () => {
  return {
    error: false,
    type: types.START,
  };
};

export const finish: () => Action = () => {
  return {
    error: false,
    type: types.FINISH,
  };
};

export const setActive = (isActive: boolean): Action => {
  return {
    error: false,
    payload: { isActive },
    type: types.SET_ACTIVE,
  };
};

export const setScanSpeed = (scanSpeed: number): Action => {
  return {
    error: false,
    payload: { scanSpeed },
    type: types.SET_SCAN_SPEED,
  };
};

export const runMiddleware = (): Action => {
  return {
    error: false,
    type: types.RUN_MIDDLEWARE,
  };
};
