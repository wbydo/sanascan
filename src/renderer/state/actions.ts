import * as types from "./types";

export interface Action {
  type: string;
  scanSpeed?: number;
}

export const increment: () => Action = () => {
  return {
    type: types.INCREMENT,
  };
};

export const startIncrement: () => Action = () => {
  return {
    type: types.START_INCREMENT,
  };
};

export const setScanSpeed = (scanSpeed: number): Action => {
  return {
    scanSpeed,
    type: types.SET_SCAN_SPEED,
  };
};
