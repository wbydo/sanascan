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
    error: true,
    type: types.START,
  };
};

export const finish: () => Action = () => {
  return {
    error: true,
    type: types.FINISH,
  };
};

export const setActive = (isActive: boolean): Action => {
  return {
    error: true,
    payload: { isActive },
    type: types.SET_ACTIVE,
  };
};

export const setScanSpeed = (scanSpeed: number): Action => {
  return {
    error: true,
    payload: { scanSpeed },
    type: types.SET_SCAN_SPEED,
  };
};

export const runMiddleware = (): Action => {
  return {
    error: true,
    type: types.RUN_MIDDLEWARE,
  };
};
