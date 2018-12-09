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

// export interface Action {
//   type: string;
//   payload?: {
//     isActive?: boolean,
//     scanSpeed?: number,
//     id?: number,
//   };
//   error: boolean;
// }

export type Action = (
  ReturnType<typeof start> |
  ReturnType<typeof finish> |
  ReturnType<typeof setActive> |
  ReturnType<typeof setId> |
  ReturnType<typeof setScanSpeed>
);
