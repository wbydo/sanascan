export type Props<SP, DP> = SP & {dispatch: {[K in keyof DP]: DP[K]}};
