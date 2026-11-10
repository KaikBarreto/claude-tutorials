// RPC dismiss_domiflix_learning_reminder · 20261031234000 (T0 v2)
import { now } from '../../core/util.mjs';

export default async function dismissDomiflixLearningReminder(_a, { db, userId }) {
  const prof = db.first('profiles', { user_id: userId });
  const today = new Date(now().getTime() - 3 * 3600e3).toISOString().slice(0, 10);
  const row = db.first('domiflix_user_onboarding', { user_id: userId });
  if (row) db.update('domiflix_user_onboarding', (r) => r === row, { dismissed_until: today });
  else db.insert('domiflix_user_onboarding', { user_id: userId, company_id: prof.company_id, window_started_at: now().toISOString(), dismissed_until: today });
  return today;
}
