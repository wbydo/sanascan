import * as types from "./types";

export const start = () => {
  return {
    error: false,
    type: types.START,
  };
};

export const kill = () => {
  return {
    error: false,
    type: types.KILL,
  };
};
