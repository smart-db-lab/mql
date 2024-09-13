
import React from 'react';
import MonacoEditor from '@monaco-editor/react';

const CustomMonacoEditor = ({ query, setQuery, setTestFile }) => {
  const handleEditorWillMount = (monaco) => {

    monaco.languages.register({ id: 'customQueryLanguage' });

    
    monaco.languages.setMonarchTokensProvider('customQueryLanguage', {
      tokenizer: {
        root: [
          [/\b(CONSTRUCT|SUPERVISED|FOR|PREDICTION|TARGET|FEATURES|ALGORITHM|TEST|FROM|GENERATE|DISPLAY|OF|WITH|ACCURACY|LABEL|CLASSIFICATION|ALGORITHMS|CLUSTERING|INSPECT|CHECKNULL|ENCODING|METHOD|TARGET-FEATURE|DEDUPLICATE|CATEGORIZE|INTO|IMPUTE|USING|STRATEGY|SHOW|AS|ON)\b/, 'keyword'],
          [/\b(LR|RF|SVR|LOG|RFC|medv|age|rad|Boston|Species|KNN|ProductID|Iris|KMeans|BostonMiss|Ordinal|One-Hot|Label|mean|L1|L2|L3|L4)\b/, 'identifier'],
          [/[0-9]+/, 'number'],
          [/[;,.]/, 'delimiter'],
          [/".*?"/, 'string'],
          [/\s+/, 'white'],
          [/[a-zA-Z_$][\w$]*/, 'identifier'],
        ]
      }
    });

   
    monaco.languages.setLanguageConfiguration('customQueryLanguage', {
      comments: {
        lineComment: '--',
        blockComment: ['/*', '*/']
      },
      brackets: [
        ['{', '}'],
        ['[', ']'],
        ['(', ')']
      ],
      autoClosingPairs: [
        { open: '{', close: '}' },
        { open: '[', close: ']' },
        { open: '(', close: ')' },
        { open: '"', close: '"' }
      ]
    });


    monaco.languages.registerCompletionItemProvider('customQueryLanguage', {
      provideCompletionItems: () => {
        const suggestions = [
          { label: 'CONSTRUCT', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'CONSTRUCT' },
          { label: 'SUPERVISED', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'SUPERVISED' },
          { label: 'FOR', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'FOR' },
          { label: 'PREDICTION', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'PREDICTION' },
          { label: 'TARGET', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'TARGET' },
          { label: 'FEATURES', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'FEATURES' },
          { label: 'ALGORITHM', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'ALGORITHM' },
          { label: 'TEST', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'TEST' },
          { label: 'FROM', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'FROM' },
          { label: 'GENERATE', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'GENERATE' },
          { label: 'DISPLAY', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'DISPLAY' },
          { label: 'OF', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'OF' },
          { label: 'WITH', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'WITH' },
          { label: 'ACCURACY', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'ACCURACY' },
          { label: 'LABEL', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'LABEL' },
          { label: 'CLASSIFICATION', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'CLASSIFICATION' },
          { label: 'ALGORITHMS', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'ALGORITHMS' },
          { label: 'CLUSTERING', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'CLUSTERING' },
          { label: 'INSPECT', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'INSPECT' },
          { label: 'CHECKNULL', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'CHECKNULL' },
          { label: 'ENCODING', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'ENCODING' },
          { label: 'METHOD', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'METHOD' },
          { label: 'TARGET-FEATURE', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'TARGET-FEATURE' },
          { label: 'DEDUPLICATE', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'DEDUPLICATE' },
          { label: 'CATEGORIZE', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'CATEGORIZE' },
          { label: 'INTO', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'INTO' },
          { label: 'IMPUTE', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'IMPUTE' },
          { label: 'USING', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'USING' },
          { label: 'STRATEGY', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'STRATEGY' },
          { label: 'SHOW', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'SHOW' },
          { label: 'AS', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'AS' },
          { label: 'ON', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'ON' },
          { label: 'KNN', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'KNN' },
          { label: 'LOG', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'LOG' },
          { label: 'SVR', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'SVR' },
          { label: 'LR', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'LR' },
          { label: 'RF', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'RF' },
          { label: 'RandomForestClassifier', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'RFC' },
          { label: 'KMeans', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'KMEANS' },
        ];
        return { suggestions };
      }
    });
  };

  return (
    <MonacoEditor
      height="300px"
      defaultLanguage="customQueryLanguage"
      value={query}
      onChange={(value) => {
        setQuery(value);
        let q = value.toLowerCase().includes(" over ");
        setTestFile(q);
      }}
      beforeMount={handleEditorWillMount}
      options={{
        selectOnLineNumbers: true,
        roundedSelection: false,
        readOnly: false,
        cursorStyle: "line",
        lineNumbers:false,
        automaticLayout: true,
        wordWrap: "on", 
        fontSize: 16    
      }}
    />
  );
};

export default CustomMonacoEditor;
