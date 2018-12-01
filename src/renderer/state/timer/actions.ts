import * as types from "./types";

export interface Action {
  type: string;
  payload?: {
    isActive?: boolean,
    scanSpeed?: number,
  };
}

export const start: () => Action = () => {
  return {
    type: types.START,
  };
};

export const finish: () => Action = () => {
  return {
    type: types.FINISH,
  };
};

export const setActive = (isActive: boolean): Action => {
  return {
    payload: { isActive },
    type: types.SET_ACTIVE,
  };
};

export const setScanSpeed = (scanSpeed: number): Action => {
  return {
    payload: { scanSpeed },
    type: types.SET_SCAN_SPEED,
  };
};
