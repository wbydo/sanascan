import * as types from "./types";

export const fetchId = (status: "start" | "done" | "error") => {
  return {
    error: status === "error",
    payload: {
      status,
    },
    type: types.FETCH_ID,
  };
};

export const setId = (id: number) => {
  return {
    error: false,
    payload: {
      id,
    },
    type: types.SET_ID,
  };
};

export const sendKey = (key: number) => {
  return {
    error: false,
    payload: {
      key,
    },
    type: types.SEND_KEY,
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

export const reset = () => {
  return {
    error: false,
    type: types.RESET,
  };
};
