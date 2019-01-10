import * as types from "./types";

export const setId = (id: number) => {
  return {
    error: false,
    payload: {
      id,
    },
    type: types.SET_ID,
  };
};

export const setResult = (result: string) => {
  return {
    error: false,
    payload: {
      content: result,
    },
    type: types.SET_RESULT,
  };
};
