import * as types from "./types";

export interface Action {
  error: boolean;
  type: string;
  payload: {
    status?: "start" | "done" | "error";
    id?: number;
    content?: string;
    key?: number; // とりあえずnumberのみ
  };
}

export const fetchId = (status: "start" | "done" | "error"): Action => {
  return {
    error: status === "error",
    payload: {
      status,
    },
    type: types.FETCH_ID,
  };
};

export const setId = (id: number): Action => {
  return {
    error: false,
    payload: {
      id,
    },
    type: types.SET_ID,
  };
};

export const sendKey = (key: number): Action => {
  return {
    error: false,
    payload: {
      key,
    },
    type: types.SEND_KEY,
  };
};

export const setResult = (result: string): Action => {
  return {
    error: false,
    payload: {
      content: result,
    },
    type: types.SET_RESULT,
  };
};
