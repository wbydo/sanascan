import { middleware as fetchIdMiddleware } from "./fetchId";
import { middleware as sendKeyMiddleware } from "./sendKey";
import { middleware as resetMiddleware } from "./reset";

export const middlewares = [
  fetchIdMiddleware,
  sendKeyMiddleware,
  resetMiddleware,
];
