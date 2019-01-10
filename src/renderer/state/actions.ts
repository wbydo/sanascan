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

export const sendKey = (key: number) => {
  return {
    error: false,
    payload: {
      key,
    },
    type: types.SEND_KEY,
  };
};

export const reset = () => {
  return {
    error: false,
    type: types.RESET,
  };
};
