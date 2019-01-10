import { Dispatch } from "redux";

import { middleware as startMiddleware } from "./start";
import { middleware as finishMiddleware } from "./finish";

import { RootState } from "../../..";

export interface Store {
  getState: () => RootState;
  dispatch: Dispatch;
}

export const middlewares = [
  startMiddleware,
  finishMiddleware,
];
