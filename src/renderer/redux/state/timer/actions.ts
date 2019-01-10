import * as types from "./types";

// 移動検討
export const start = () => {
  return {
    error: false,
    type: types.START,
  };
};

// 移動検討
export const finish = (id?: number) => {
  return {
    error: false,
    payload: { id },
    type: types.FINISH,
  };
};

export const setActive = (isActive: boolean) => {
  return {
    error: false,
    payload: { isActive },
    type: types.SET_ACTIVE,
  };
};

export const setId = (id: number) => {
  return {
    error: false,
    payload: { id },
    type: types.SET_ID,
  };
};

export const setScanSpeed = (scanSpeed: number) => {
  return {
    error: false,
    payload: { scanSpeed },
    type: types.SET_SCAN_SPEED,
  };
};
