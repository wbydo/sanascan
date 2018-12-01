import * as types from "./types";

export interface Action {
  error: boolean;
  type: string;
  payload?: {
    isActive?: boolean;
    scanSpeed?: number;
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

export const setScanSpeed = (scanSpeed: number): Action => {
  return {
    error: false,
    payload: {
      scanSpeed,
    },
    type: types.SET_SCAN_SPEED,
  };
};
