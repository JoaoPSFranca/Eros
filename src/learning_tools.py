import json
import os
from datetime import datetime
import random
from collections import Counter

class LearningTools:
    def __init__(self, ai_engine):
        self.ai_engine = ai_engine
        self.feedback_file = "data/ai/feedback.json"
        self.conversations_file = "data/ai/conversations.json"
        self.suggested_intents_file = "data/ai/suggested_intents.json"
        self.setup_learning()

    def setup_learning(self):
        try:
            os.makedirs('data/ai', exist_ok=True)

            if not os.path.exists(self.feedback_file):
                with open(self.feedback_file, 'w', encoding='utf-8') as f:
                    json.dump([], f)

            if not os.path.exists(self.conversations_file):
                with open(self.conversations_file, 'w', encoding='utf-8') as f:
                    json.dump([], f)

            if not os.path.exists(self.suggested_intents_file):
                with open(self.suggested_intents_file, 'w', encoding='utf-8') as f:
                    json.dump([], f)

        except Exception as e:
            print(f"Erro ao configurar ferramentas de aprendizado: {e}")

    def save_conversation(self, user_input, assistant_response):
        try:
            with open(self.conversations_file, 'r', encoding='utf-8') as f:
                conversations = json.load(f)

            conversations.append({
                "timestamp": datetime.now().isoformat(),
                "user_input": user_input,
                "assistant_response": assistant_response
            })

            with open(self.conversations_file, 'w', encoding='utf-8') as f:
                json.dump(conversations, f, indent=4, ensure_ascii=False)

            self.analyze_conversation(user_input, assistant_response)

        except Exception as e:
            print(f"Erro ao salvar conversa: {e}")

    def save_feedback(self, user_input, assistant_response, feedback_score, new_response=None):
        try:
            with open(self.feedback_file, 'r', encoding='utf-8') as f:
                feedback_data = json.load(f)

            feedback_entry = {
                "timestamp": datetime.now().isoformat(),
                "user_input": user_input,
                "assistant_response": assistant_response,
                "feedback_score": feedback_score
            }

            if new_response:
                feedback_entry["better_response"] = new_response

            feedback_data.append(feedback_entry)

            with open(self.feedback_file, 'w', encoding='utf-8') as f:
                json.dump(feedback_data, f, indent=4, ensure_ascii=False)

            if feedback_score >= 4 and assistant_response:
                tag, confidence = self.ai_engine.predict_intent(user_input)

                if confidence < 0.7 and tag:
                    with open(self.suggested_intents_file, 'r', encoding='utf-8') as f:
                        suggested_intents = json.load(f)

                    suggested_intents.append({
                        "tag": tag,
                        "pattern": user_input,
                        "response": assistant_response,
                        "confidence": confidence,
                        "timestamp": datetime.now().isoformat()
                    })

                    with open(self.suggested_intents_file, 'w', encoding='utf-8') as f:
                        json.dump(suggested_intents, f, indent=4, ensure_ascii=False)


        except Exception as e:
            print(f"Erro ao salvar feedback: {e}")

    def analyze_conversation(self, user_input, assistant_response):
        try:
            tag, confidence = self.ai_engine.predict_intent(user_input)

            if confidence < 0.3:
                with open(self.conversations_file, 'r', encoding='utf-8') as f:
                    conversations = json.load(f)

                similar_responses = []
                for conv in conversations:
                    if conv["assistant_response"] == assistant_response and conv["user_input"] != user_input:
                        similar_responses.append(conv["user_input"])

                if similar_responses:
                    with open(self.suggested_intents_file, 'r', encoding='utf-8') as f:
                        suggested_intents = json.load(f)

                    suggested_tag = "auto_" + str(len(suggested_intents) + 1)

                    suggested_intents.append({
                        "suggested_tag": suggested_tag,
                        "patterns": [user_input] + similar_responses[:3],  # Limitamos a 3 padrões similares
                        "responses": [assistant_response],
                        "timestamp": datetime.now().isoformat(),
                        "auto_detected": True
                    })

                    with open(self.suggested_intents_file, 'w', encoding='utf-8') as f:
                        json.dump(suggested_intents, f, indent=4, ensure_ascii=False)

        except Exception as e:
            print(f"Erro ao analisar conversa: {e}")

    def analyze_learning_data(self):
        try:
            with open(self.feedback_file, 'r', encoding='utf-8') as f:
                feedback_data = json.load(f)

            with open(self.conversations_file, 'r', encoding='utf-8') as f:
                conversations = json.load(f)

            with open(self.suggested_intents_file, 'r', encoding='utf-8') as f:
                suggested_intents = json.load(f)

            if len(conversations) < 10:
                return "Dados insuficientes para análise."

            user_inputs = [conv["user_input"] for conv in conversations]
            all_words = []

            for input_text in user_inputs:
                words = [word.lower() for word in input_text.split() if len(word) > 3]
                all_words.extend(words)

            word_counter = Counter(all_words)
            top_words = word_counter.most_common(10)

            negative_feedback = [item for item in feedback_data if item.get("feedback_score", 0) < 3]
            learning_opportunities = []

            for item in negative_feedback:
                if "better_response" in item:
                    learning_opportunities.append({
                        "input": item["user_input"],
                        "current_response": item["assistant_response"],
                        "better_response": item["better_response"]
                    })

            unrecognized_patterns = {}
            for conv in conversations:
                tag, confidence = self.ai_engine.predict_intent(conv["user_input"])
                if confidence < 0.4:
                    if tag not in unrecognized_patterns:
                        unrecognized_patterns[tag] = []
                    unrecognized_patterns[tag].append(conv["user_input"])

            report = "Análise de aprendizado:\n\n"

            report += f"Conversas analisadas: {len(conversations)}\n"
            report += f"Feedbacks recebidos: {len(feedback_data)}\n"
            report += f"Sugestões de intents: {len(suggested_intents)}\n\n"

            report += "Palavras mais comuns nas conversas:\n"
            for word, count in top_words:
                report += f"- {word}: {count} ocorrências\n"

            report += f"\nOportunidades de aprendizado ({len(learning_opportunities)}):\n"
            for i, opportunity in enumerate(learning_opportunities[:5], 1):
                report += f"{i}. Input: \"{opportunity['input']}\"\n"
                report += f"   Resposta atual: \"{opportunity['current_response']}\"\n"
                report += f"   Resposta melhor: \"{opportunity['better_response']}\"\n"

            report += f"\nPadrões não reconhecidos ({sum(len(patterns) for patterns in unrecognized_patterns.values())}):\n"
            for tag, patterns in unrecognized_patterns.items():
                report += f"- Tag: {tag or 'Desconhecida'} ({len(patterns)} ocorrências)\n"
                for pattern in patterns[:3]:
                    report += f"  - \"{pattern}\"\n"

            report += f"\nSugestões de novos intents ({len(suggested_intents)}):\n"
            for i, suggestion in enumerate(suggested_intents[:5], 1):
                report += f"{i}. Tag sugerida: {suggestion.get('suggested_tag') or suggestion.get('tag', 'Desconhecida')}\n"
                report += f"   Padrões: {', '.join(suggestion.get('patterns', [suggestion.get('pattern', '')]))}\n"
                report += f"   Respostas: {', '.join(suggestion.get('responses', [suggestion.get('response', '')]))}\n"

            return report

        except Exception as e:
            print(f"Erro na análise de dados: {e}")
            return f"Erro ao analisar dados de aprendizado: {e}"

    def apply_suggested_intents(self, max_suggestions=5):
        try:
            with open(self.suggested_intents_file, 'r', encoding='utf-8') as f:
                suggested_intents = json.load(f)

            if not suggested_intents:
                return "Nenhuma sugestão de intent disponível."

            suggested_intents.sort(key=lambda x: x.get('timestamp', ''), reverse=True)

            applied_count = 0
            for suggestion in suggested_intents[:max_suggestions]:
                if 'auto_detected' in suggestion and suggestion['auto_detected']:
                    tag = suggestion.get('suggested_tag', f"auto_{datetime.now().strftime('%Y%m%d%H%M%S')}")
                    patterns = suggestion.get('patterns', [])
                    responses = suggestion.get('responses', [])
                else:
                    tag = suggestion.get('tag', f"feedback_{datetime.now().strftime('%Y%m%d%H%M%S')}")
                    patterns = [suggestion.get('pattern', '')]
                    responses = [suggestion.get('response', '')]

                if patterns and responses and tag:
                    success = self.ai_engine.add_training_data(tag, patterns, responses)
                    if success:
                        applied_count += 1

            if applied_count > 0:
                suggested_intents = suggested_intents[applied_count:]
                with open(self.suggested_intents_file, 'w', encoding='utf-8') as f:
                    json.dump(suggested_intents, f, indent=4, ensure_ascii=False)

            return f"Aplicadas {applied_count} sugestões de intents ao treinamento da IA."

        except Exception as e:
            print(f"Erro ao aplicar sugestões de intents: {e}")
            return f"Erro ao aplicar sugestões: {e}"