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

// ////////////////////////////////////////////
// timer

export const startTimer: () => Action = () => {
  return {
    type: types.START_TIMER,
  };
};

export const finishTimer: () => Action = () => {
  return {
    type: types.FINISH_TIMER,
  };
};

// timer
// ////////////////////////////////////////////

export const setScanSpeed = (scanSpeed: number): Action => {
  return {
    scanSpeed,
    type: types.SET_SCAN_SPEED,
  };
};

export const activateConfigure: () => Action = () => {
  return {
    type: types.ACTIVATE_CONFIGURE,
  };
};

export const deactivateConfigure: () => Action = () => {
  return {
    type: types.DEACTIVATE_CONFIGURE,
  };
};
