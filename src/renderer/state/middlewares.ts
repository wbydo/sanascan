import { timerMiddleware } from "./timer/index";
import { estimatorMiddleware } from "./estimator";

const middlewares = [
  timerMiddleware,
  estimatorMiddleware,
];

export default middlewares;
