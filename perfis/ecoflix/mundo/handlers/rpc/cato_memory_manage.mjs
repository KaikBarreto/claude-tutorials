// Memória do Cato: ligada, sem memórias guardadas (o mundo não tem conversa anterior com o assistente).
export default (a) => ({
  enabled: true, epoch: 1, sharedEnabled: true, sharedEpoch: 1, canManage: true,
  preferenceRetentionDays: 90, topicRetentionDays: 30,
  ...(a?.p_action === 'list' ? { memories: [], hasMore: false } : {}),
});
