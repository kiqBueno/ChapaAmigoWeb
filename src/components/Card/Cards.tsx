import Card from "./Card";

const Cards = () => (
  <div className="cardsContainer">
    <div className="cards">
      <Card
        title="Conexão Direta"
        content="Na Plataforma Chapa Amigo, a conexão é direta e eficiente. Converse diretamente com caminhoneiros e transportadoras, eliminando intermediários e garantindo negociações transparentes. Com suporte eficiente, organização de serviços, localização precisa e comunicação direta, proporcionando praticidade e confiabilidade em sua rotina."
      />
      <Card
        title="Negociação Transparente"
        content="Defina seus preços, encontre as melhores oportunidades para sua rota e disponibilidade, e tenha controle total do valor combinado. Seu negócio, suas regras!"
      />
      <Card
        title="Segurança em Primeiro Lugar"
        content="A Plataforma Chapa Amigo oferece um ambiente seguro e profissional para a realização de negociações. A verificação de perfis, o canal de comunicação exclusivo e o registro de Ordens de Serviços garantem a proteção dos usuários e a integridade das transações."
      />
    </div>
    <div className="cards">
      <Card
        title="Flexibilidade Total, Seu Tempo, Suas Escolhas!"
        content="Amigo Chapa, aqui você decide quando e como quer trabalhar. A plataforma está sempre disponível para te conectar com novas oportunidades, mas a decisão de aceitar ou não é sempre sua."
      />
      <Card
        title="Acesso Total por um Preço Justo"
        content="Com uma mensalidade acessível, você tem acesso ilimitado a todas as funcionalidades do nosso aplicativo e pode participar quando e como quiser."
      />
      <Card
        title="Sem Surpresas Desagradáveis, Seu Dinheiro na Mão!"
        content="Na Plataforma Chapa Amigo, você sabe exatamente quanto vai receber pelo seu trabalho. Sem taxas escondidas ou comissões inesperadas, o valor combinado é seu!"
      />
    </div>
  </div>
);

export default Cards;
