import * as types from "./types";

export const start = () => {
  return {
    error: false,
    type: types.START,
  };
};

export const finish = (id?: number) => {
  return {
    error: false,
    payload: { id },
    type: types.FINISH,
  };
};
