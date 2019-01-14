import * as types from "./types";

export const setActive = (isActive: boolean) => {
  return {
    error: false,
    payload: { isActive },
    type: types.SET_ACTIVE,
  };
};

export const setScanSpeed = (scanSpeed: number) => {
  return {
    error: false,
    payload: { scanSpeed },
    type: types.SET_SCAN_SPEED,
  };
};
